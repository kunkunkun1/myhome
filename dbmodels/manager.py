from django.db import models

class IndexManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stat=1)


class ShowImgManager(IndexManager):
    def get_slider(self):
        return self.get_queryset().filter(img_type=0,
                                transcation__stat=1).values(
                                'transcation__img').order_by(
                                '-top','-transcation__create_time')


class RightNavManager(IndexManager):
    def get_title(self):
        return self.get_queryset().values('title','icon').order_by('pk')

class MenuManager(IndexManager):
    def get_menu(self):
        parent_list = self.get_queryset().filter(parent_menu__isnull=True).order_by('pk')

        result = []
        for parent in parent_list:
            data = {}
            data['title'] = parent.title
            data['menu'] = list(parent.child.values('id','title','url'))

            result.append(data)

        return result


class TransactionManager(IndexManager):
    def get_transaction(self,**kwargs):
        return self.get_queryset().filter(**kwargs).values('id','team',).order_by('-create_time')
