from io import BytesIO

import qrcode as qc
from PIL import ImageDraw, Image
from django.core.files import File
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)

from core.settings import BASE_URL
# from faker_data import initialization
from src.accounts.models import User
from src.administration.admins.filters import UserFilter, ProductFilter, InvoiceFilter
from src.administration.admins.models import Product, Invoice, InvoiceItem

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(TemplateView):
    """
    Registrations: Today, Month, Year (PAID/UNPAID)
    Subscriptions: Today, Month, Year (TYPES)
    Withdrawals  : Today, Month, Year (CALCULATE)
    """
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        # context = calculate_statistics(context)
        # initialization(init=False, mid=False, end=False)
        return context


""" USERS """


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admins/user_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user_filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['user_filter_form'] = user_filter.form

        paginator = Paginator(user_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['user_list'] = user_page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        'profile_image', 'first_name', 'last_name',
        'email', 'username', 'phone_number', 'is_active'
    ]
    template_name = 'admins/user_update_form.html'

    def get_success_url(self):
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})


@method_decorator(admin_decorators, name='dispatch')
class UserPasswordResetView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/admin_password_reset.html', {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
        return render(request, 'admins/admin_password_reset.html', {'form': form})


""" PRODUCTS """


@method_decorator(admin_decorators, name='dispatch')
class ProductListView(ListView):
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        object_filter = ProductFilter(self.request.GET, queryset=Product.objects.filter())
        context['filter_form'] = object_filter.form

        paginator = Paginator(object_filter.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('admins:product-list')


@method_decorator(admin_decorators, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('admins:product-list')


@method_decorator(admin_decorators, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admins:product-list')


""" INVOICES """


@method_decorator(admin_decorators, name='dispatch')
class InvoiceListView(ListView):
    queryset = Invoice.objects.all()

    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        object_filter = InvoiceFilter(self.request.GET, queryset=Invoice.objects.filter())
        context['filter_form'] = object_filter.form

        paginator = Paginator(object_filter.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class InvoiceCreateView(CreateView):
    model = Invoice
    fields = '__all__'
    success_url = reverse_lazy('admins:invoice-list')


@method_decorator(admin_decorators, name='dispatch')
class InvoiceUpdateView(UpdateView):
    model = Invoice
    fields = '__all__'
    success_url = reverse_lazy('admins:invoice-list')


class InvoiceDetailView(DetailView):
    model = Invoice


@method_decorator(admin_decorators, name='dispatch')
class InvoiceDeleteView(DeleteView):
    model = Invoice
    success_url = reverse_lazy('admins:invoice-list')


@method_decorator(admin_decorators, name='dispatch')
class InvoicerView(View):
    template_name = "admins/invoicer.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        data = dict(request.POST)
        customer_name = data['customer_name'][0]
        address = data['address'][0]
        company_name = data['company_name'][0]
        company_description = data['company_description'][0]

        if not request.POST.get('p-id'):
            messages.error(request, "No products selected for now.")

        else:
            products_qty = data['p-qty']
            products_id = data['p-id']
            products_vat = data['p-vat']
            products_amount = data['p-amount']
            size = len(products_id)

            invoice = Invoice(
                customer_name=customer_name,
                address=address,
                company_name=company_name,
                company_description=company_description,
            )

            invoice.total = data['total'][0]
            invoice.vat = data['vat-total'][0]
            invoice.grand_total = data['grand-total'][0]
            invoice.save()

            qr_code_img = qc.make(f"{BASE_URL}/admins/invoice/{invoice.pk}/")
            canvas = Image.new("RGB", (380, 380), "white")
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qr_code_img)
            buffer = BytesIO()
            canvas.save(buffer, "PNG")
            invoice.qr_image.delete(save=True)
            invoice.qr_image.save(f'qr_image_{invoice.pk}.png', File(buffer), save=True)
            canvas.close()

            for index in range(size):
                product = Product.objects.get(pk=products_id[index])
                InvoiceItem(
                    invoice=invoice, product=product,
                    amount=products_amount[index], quantity=products_qty[index], vat=products_vat[index]
                ).save()

            messages.success(request, "Invoice created successfully.")

        return render(request, self.template_name)
