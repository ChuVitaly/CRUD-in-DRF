from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']




class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:

        model = StockProduct
        fields = ['id', 'quantity', 'price', 'product']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']


    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(stock_id=stock.id, **position)

        return stock


    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        StockProduct.objects.filter(stock_id=instance.id).delete()
        for position in positions:
            StockProduct.objects.create(stock_id=stock.id, **position)


        return stock