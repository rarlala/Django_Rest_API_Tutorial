import random

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from members.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetTest(APITestCase):
    """
    PostMan이 하는 일을 코드로 자동화
    DB는 분리됨
    """

    def test_snippet_list(self):
        url = '/api-view/snippets/'
        # self.client = requests와 같은 역할
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # 5개의 Snippet을 만들고 응답의 객체 개수 비교
        # user = User.objects.create(username='test')
        baker.make(Snippet, _quantity=5)
        # user = baker.make(User)
        # for i in range(5):
        #     Snippet.objects.create(code='1', author=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),5)

        for snippet_data in response.data:
            self.assertIn('author', snippet_data)
            self.assertIn('title', snippet_data)
            self.assertIn('code', snippet_data)
            self.assertIn('linenos', snippet_data)
            self.assertIn('language', snippet_data)
            self.assertIn('style', snippet_data)

            # self.assertEquel('1', snippet_data['code'])

            # 전달된 Snippet object(dict)의 'pk'에 해당하는
            # 실제 Snippet model instance를
            # SnippetSerializer를 통해 serialize한 값과 snippet_data가 같은지 비교
            pk = snippet_data['pk']
            snippet = Snippet.objects.get(pk=pk)
            self.assertEqual(
                SnippetSerializer(snippet).data,
                snippet_data
            )

    def test_snippet_create(self):
        """
        Snippet객체를 만든다.
        """

        url = '/api-view/snippets/'

        # Snippet 객체를 만들기 위해 클라이언트로부터 전달될 JSON 객체를 Parse한 Python 객체
        user = baker.make(User)
        data = {
            'author': user.pk,
            'code': 'def test():',
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 응답에 돌아온 객체가 SnippetSerializer로
        # 실제 Model instance를 serializer한 결과와 같은지 확인
        pk = response.data['pk']
        snippet = Snippet.objects.get(pk=pk)
        self.assertEqual(response.data, SnippetSerializer(snippet).data,)

        # 객체를 하나 생성했으니, 전체 Snippet 객체의 개수가 1개인지 확인(ORM)
        self.assertEqual(Snippet.objects.count(), 1)

    def test_snippet_delete(self):
        # 미리 객체를 5개 만들어 놓는다.
        # delete API를 적절히 실행 한 후, 객체가 4개가 되었는지 확인
        # 지운 객체가 실제로 존재하지 않는지 확인
        snippets = baker.make(Snippet, _quantity=5)
        snippet = random.choice(snippets)
        # user = User.objects.create(username='test')
        # snippets = [Snippet.objects.create(code='1', author=user) for i in range(5)]
        # self.assertEqual(Snippet.objects.count(), 5)

        # snippet = random.choice(snippets)
        url = f'/api-view/snippets/{snippet.pk}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 4)
        self.assertFalse(Snippet.objects.filter(pk=snippet.pk).exists())
