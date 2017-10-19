from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import PointTransaction


class PointCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=101)

        user = request.user
        amount = request.POST.get('amount')
        type = request.POST.get('type')

        try:
            trans = PointTransaction.objects.create_new(
                user=user,
                amount=amount,
                type=type
            )
            print("33" + trans)
        except:
            trans = None

        if trans is not None:
            data = {
                "works": True,
                "merchant_id": trans
            }
            print(data)
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


class PointImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)

        user = request.user
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        # print("@@@@@: " + user)
        # print("@@@@@: " + merchant_id)
        # print("@@@@@: " + imp_id)
        # print("@@@@@: " + amount)

        try:
            trans = PointTransaction.objects.get(
                user=user,
                order_id=merchant_id,
                amount=amount
            )
            # print("@@@@@: " + trans)
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()

            data = {
                "works": True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


def charge_point(request):
    template = 'billing/charge.html'

    return render(request, template)
