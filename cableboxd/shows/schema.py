import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField

from .models import Show, SeenList
from users.schema import UserType


class ShowType(DjangoObjectType):
    class Meta:
        model = Show

class SeenListType(DjangoObjectType):
    class Meta:
        model = SeenList


class CreateShow(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    years = graphene.String()
    poster = graphene.String()
    rating = graphene.String()
    summary = graphene.String()
    creators = graphene.String()
    stars = graphene.String()

   
    class Arguments:
        title = graphene.String()
        years = graphene.String()
        poster = graphene.String()
        rating = graphene.String()
        summary = graphene.String()
        creators = graphene.String()
        stars = graphene.String()

    
    def mutate(self, info, title, years, poster, rating, summary, creators, stars):
        show = Show(title = title, years = years, poster = poster, rating = rating, summary = summary, creators = creators, stars = stars)
        show.save()

        return CreateShow(
            id=show.id,
            title = show.title,
            years = show.years,
            poster = show.poster,
            rating = show.rating,
            summary = show.summary,
            creators = show.creators,
            stars = show.stars,
        )

class CreateSeenList(graphene.Mutation):
    user = graphene.Field(UserType)
    show = graphene.Field(ShowType)

    class Arguments:
        show_id = graphene.Int()

    def mutate(self, info, show_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to add to your list!')

        show = Show.objects.filter(id=show_id).first()
        if not show:
            raise Exception('Invalid Link!')

        SeenList.objects.create(
            user=user,
            show=show,
        )

        return CreateSeenList(user=user, show=show)
        


class Query(graphene.ObjectType):
    shows = graphene.List(ShowType, title=graphene.String(), star=graphene.String(), 
    years=graphene.String(), first=graphene.Int(), skip=graphene.Int(), search=graphene.String())
    seenlist = graphene.List(SeenListType, id=graphene.Int())

    
            
    def resolve_shows(self, info, **kwargs):
        title = kwargs.get("title")
        years = kwargs.get("years")
        star = kwargs.get("star")
        first = kwargs.get("first")
        skip = kwargs.get("skip")
        search = kwargs.get("search")

        qs = Show.objects.all()
        if search:
            filter = (
                Q(title__icontains=search)|
                Q(stars__icontains=search)|
                Q(creators__icontains=search)
            )
            qs = qs.filter(filter)
            #a search will return matching titles, stars, creators with arg = 'search:_____'

        if title:
            filter = (
                Q(title__icontains=title) 
            )
            qs = qs.filter(filter)
            # { 
            # shows(title: "Breaking"){
            #     title
            #     years
            #     poster
            #     rating
            #     summary
            #     creators
            #     stars
            # }
            # }
        if star:
            filter = (
                Q(stars__icontains=star)                
            )
            qs = qs.filter(filter)
        if years:
            filter=(
                Q(years__icontains=years)
            )
            qs = qs.filter(filter)
            # { 
            #   shows(years: "2006"){
            #     title
            #     years
            #     poster
            #     rating
            #     summary
            #     creators
            #     stars
            #   }
            # }
        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]
        # {  
        # shows(first: 2, skip:4){
        #     title
        #     years
        #     poster
        #     rating
        #     summary
        #     creators
        #     stars
        # }}
        # RETURNS THE NEXT 2 VALUES STARTING AT 4
        return qs
        # {
        # shows{
        #     title
        #     years
        #     poster
        #     rating
        #     summary
        #     creators
        #     stars
        # }
        # }

    def resolve_seenlist(self, info,  **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return SeenList.objects.filter(user__id=id)          
            # {
            #   seenlist (id:4){   ID OPTIONAL
            #     id
            #     user {
            #       id
            #       username
            #     }
            #     show {
            #       id
            #       title
            #     }
            #   }
            # }
        return SeenList.objects.all()
      



class Mutation(graphene.ObjectType):
    create_show = CreateShow.Field()
    create_seenlist = CreateSeenList.Field()