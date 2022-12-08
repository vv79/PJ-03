from django.urls import path
from django.contrib.auth.decorators import login_required


from .views import (
   HomePage,
   AnnouncementList,
   AnnouncementCategorySubscribe,
   AnnouncementCategoryUnsubscribe,
   AnnouncementSearch,
   AnnouncementDetail,
   AnnouncementCreate,
   AnnouncementUpdate,
   AnnouncementDelete,
   ResponseList,
   ResponseCreate,
   ResponseDetail,
   ResponseApprove,
   ResponseDelete
)

urlpatterns = [
   path('', HomePage.as_view(), name='homepage'),

   path('announcement/', AnnouncementList.as_view(), name='announcement_list'),
   path('announcement/category/<int:category>', AnnouncementList.as_view(), name='announcement_category'),
   path(
      'announcement/category/<int:category>/subscribe',
      login_required(AnnouncementCategorySubscribe.as_view()),
      name='announcement_category_subscribe'
   ),
   path(
      'announcement/category/<int:category>/unsubscribe',
      login_required(AnnouncementCategoryUnsubscribe.as_view()),
      name='announcement_category_unsubscribe'
   ),
   path('announcement/<int:pk>/', AnnouncementDetail.as_view(), name='announcement_detail'),
   path('announcement/search/', AnnouncementSearch.as_view(), name='announcement_search'),
   path('announcement/create/', AnnouncementCreate.as_view(), name='announcement_create'),
   path('announcement/<int:pk>/edit/', AnnouncementUpdate.as_view(), name='announcement_edit'),
   path('announcement/<int:pk>/delete/', AnnouncementDelete.as_view(), name='announcement_delete'),

   path('response/', login_required(ResponseList.as_view()), name='response_list'),
   path('response/announcement/<int:announcement>', login_required(ResponseList.as_view()), name='response_announcement'),
   path('response/<announcement>/create/', login_required(ResponseCreate.as_view()), name='response_create'),
   path('response/<int:pk>/', login_required(ResponseDetail.as_view()), name='response_detail'),
   path('response/<int:pk>/approve/', login_required(ResponseApprove.as_view()), name='response_approve'),
   path('response/<int:pk>/delete/', login_required(ResponseDelete.as_view()), name='response_delete'),
]
