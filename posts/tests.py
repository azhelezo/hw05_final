import os
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .models import Follow, Group, Post, User
from yatube.settings import BASE_DIR

TEST_TEXT = 'Hasta la vista'
TEST_EDIT = 'Ill be back'


class TestPosts(TestCase):
    def setUp(self):
        cache.clear()  # clear cache before test start
        self.anon_client = Client()
        self.user_client = Client()
        self.user = User.objects.create_user(username='terminator', password='skynetMyLove')
        self.user2 = User.objects.create_user(username='bender', password='KillAllHoomans')
        self.user3 = User.objects.create_user(username='bart', password='iwillnotshitpost')
        self.user_client.login(username=self.user.username, password='skynetMyLove')
        self.group = Group.objects.create(
            title='skynet',
            slug='skynet',
            description='Death to all humans!'
            )
        self.test_post = Post.objects.create(
            text=TEST_TEXT,
            author=self.user,
            group=self.group
            )  # create new post

    def post_test(self, post, compare_text):  # test a post
        self.assertEqual(post.text, compare_text)  # post has correct text
        self.assertEqual(post.group, self.group)  # post has correct group
        response = self.user_client.get(reverse('index'))
        self.assertContains(response, post.text, status_code=200)  # post in index
        response = self.user_client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, post.text, status_code=200)  # post in profile
        response = self.user_client.get(reverse('post', args=[self.user.username, post.id]))
        self.assertContains(response, post.text, status_code=200)  # post in post page

    def test_profile_created(self):  # profile
        response = self.user_client.get(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)  # profile page existst

    def test_auth_new_post(self):  # new
        response = self.user_client.get(reverse('new_post'), follow=False)
        self.assertEqual(response.status_code, 200)  # user has access to new_post

    def test_anon_new_post(self):  # redirect
        posts_count = Post.objects.all().count()  # count posts before anon post attempt
        response = self.anon_client.post(
            reverse('new_post'),
            {'text': TEST_TEXT},
            follow=True
            )  # @login_required works, anon redirected to login
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('new_post'))
        self.assertEquals(posts_count, Post.objects.all().count())  # count of posts not changed

    def test_auth_post_created(self):  # post on pages
        self.post_test(self.test_post, TEST_TEXT)

    def test_auth_post_edited(self):  # post updates
        response = self.user_client.post(
            reverse('post_edit', args=[self.user.username, self.test_post.id]),
            {'text': TEST_EDIT, 'group': self.group.id},
            follow=True
            )
        self.post_test(response.context['post'], TEST_EDIT)

    def test_not_found(self):
        response = self.user_client.get('/ololo/')
        self.assertEqual(response.status_code, 404)

    def test_img_in_post(self):
        test_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x01\x00\x3b'
        )
        img = SimpleUploadedFile(
            name='some.gif',
            content=test_gif,
            content_type='image/gif',
        )
        img_post = Post.objects.create(
            author=self.user,
            text='post with image',
            group=self.group,
            image=img,
        )

        urls = [
            reverse('index'),
            reverse('profile', args=[self.user.username]),
            reverse('post', args=[self.user.username, img_post.id]),
            reverse('group', args=[img_post.group]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(url)
                self.assertContains(response, '<img')
        
        os.remove(os.path.join(BASE_DIR, 'media/posts/some.gif'))

    def test_not_img_in_post(self):
        txt = SimpleUploadedFile(
            name='some.txt',
            content=b'aaa',
            content_type='text/plain',
        )

        url = reverse('new_post')
        response = self.user_client.post(url, {'text': 'not img', 'image': txt})

        self.assertFormError(
            response,
            'form',
            'image',
            errors=(
                'Загрузите правильное изображение. '
                'Файл, который вы загрузили, поврежден '
                'или не является изображением.'
                ),
        )

    def test_index_cache(self):
        response = self.user_client.get(reverse('index'))
        self.assertNotContains(response, 'cache')
        Post.objects.create(author=self.user, text='cache')
        self.assertNotContains(response, 'cache')
        response = self.user_client.get(reverse('index'))
        self.assertContains(response, 'cache')

    def test_user_can_subscribe(self):
        self.user_client.post(reverse('profile_follow', args=[self.user2]))
        self.assertTrue(Follow.objects.filter(user=self.user, author=self.user2).exists())

    def test_user_can_unsubscribe(self):
        Follow.objects.create(user=self.user, author=self.user2)
        self.user_client.post(reverse('profile_unfollow', args=[self.user2]))
        self.assertFalse(Follow.objects.filter(user=self.user, author=self.user2).exists())

    def test_post_shows_if_following(self):
        Follow.objects.create(user=self.user, author=self.user2)
        Post.objects.create(text='sub test', author=self.user2)
        response = self.user_client.get(reverse('follow_index'))
        self.assertContains(response, 'sub test')

    def test_post_shows_if_not_following(self):
        Post.objects.create(text='sub test', author=self.user2)
        self.user3_client = Client()
        self.user3_client.force_login(self.user3)
        self.assertFalse(Follow.objects.filter(author=self.user2, user=self.user3).exists())
        response = self.user3_client.get(reverse('follow_index'))
        self.assertNotContains(response, 'sub test')

    def test_only_user_can_comment(self):
        self.user_client.post(reverse(
            'add_comment',
            args=[self.user.username, self.test_post.id]),
            {'text': 'test comment'}
            )
        response = self.user_client.get(reverse('post', args=[self.user.username, self.test_post.id]))
        self.assertContains(response, 'test comment')
        self.anon_client.post(reverse(
            'add_comment',
            args=[self.user.username, self.test_post.id]),
            {'text': 'anon comment'}
            )
        response = self.anon_client.get(reverse('post', args=[self.user.username, self.test_post.id]))
        self.assertContains(response, 'test comment')
        self.assertNotContains(response, 'anon comment')
