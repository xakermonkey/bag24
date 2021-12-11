from django.shortcuts import render


# Create your views here.


def AdminPanel(request):
    return render(request, 'keepit_admin/admin_panel.html')


def AdminPostDetail(request, pk):
    return render(request, 'keepit_admin/keepit_detail.html')


def AdminPostHistory(request, pk):
    return render(request, 'keepit_admin/keepit_postmat_history.html')


def AdminPostClearHistory(request, pk):
    return render(request, 'keepit_admin/keepit_postamat_clear_history.html')
