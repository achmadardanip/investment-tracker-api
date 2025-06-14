import graphene
from graphene_django import DjangoObjectType

from .models import Investment

class InvestmentType(DjangoObjectType):
    class Meta:
        model = Investment
        fields = ("id", "asset_name", "current_value")

class Query(graphene.ObjectType):
    portfolio = graphene.List(InvestmentType, user_id=graphene.ID(required=True))

    def resolve_portfolio(root, info, user_id):
        return Investment.objects.filter(user_id=user_id)

class Mutation(graphene.ObjectType):
    create_investment = graphene.Field(InvestmentType,
                                      asset_name=graphene.String(required=True),
                                      amount_invested=graphene.Float(required=True))

    def resolve_create_investment(root, info, asset_name, amount_invested):
        user = info.context.user
        investment = Investment.objects.create(
            user=user,
            asset_name=asset_name,
            amount_invested=amount_invested,
            purchase_date=info.context.request.timestamp if hasattr(info.context.request, 'timestamp') else None,
            current_value=amount_invested,
        )
        return investment

schema = graphene.Schema(query=Query, mutation=Mutation)
