from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django import forms


# Create your views here.

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Information contact - Online Store",
            "subtitle": "Contact",
            "email": "Email: contact@contact.com",
            "number": "Phone: +57 123 456 7890",
            "address": "Address: Cra 999a#00-00"
        })
        return context

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "tittle": "About_Us - Online Store",
            "subtitle": "About Us",
            "description": "This is an about page...",
            "author": "Developed by: Juan Pablo Jimenez Quiroz",
        })
        return context
    
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 500.0},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 1000.0},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 35.0},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 150.0},
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of Products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)   
    
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        if id.isdigit() and int(id) > 0 and int(id) <= len(Product.products):
            product = Product.products[int(id)-1]
        else:
            return HttpResponseRedirect(reverse('home'))
        viewData["title"] = product["name"] + "- Online Store"
        viewData["subtitle"] = product["description"] + " - Product Information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("The price must be greater than zero.")
        return price
    

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create Product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            new_id = str(len(Product.products) + 1)
            product = {
                "id": new_id,
                "name": form.cleaned_data['name'],
                "price": form.cleaned_data['price'],
                "description": form.cleaned_data.get('description', ""),
            }
            Product.products.append(product)
            viewData = {
                "title": "Product Created",
                "product": product
            }
            return render(request, 'products/created.html', viewData)
        else:
            viewData = {}
            viewData["title"] = "Create Product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)