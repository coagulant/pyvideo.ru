# coding: utf-8
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView
from haystack.query import SearchQuerySet
from richard.videos.models import Speaker, Category, Video, Tag


class SpeakerList(ListView):
    template_name = 'videos/speaker_list.html'
    context_object_name = 'speakers'
    queryset = Speaker.objects.annotate(video_count=Count('videos'))


def home(request):
    latest_categories = Category.objects.order_by('-added')[:10]
    latest_videos = Video.objects.live().order_by('-added')[:10]

    video_count = Video.objects.live().count()

    ret = render(
        request, 'home_branded.html',
        {'title': settings.SITE_TITLE,
         'latest_categories': latest_categories,
         'latest_videos': latest_videos,
         'video_count': video_count,
         'tags': Tag.objects.exclude(tag__in=['Lightning talk']).annotate(num_videos=Count('videos'))
        })
    return ret


def search(request):
    q = request.GET.get('q', '')
    cat_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    facet_counts = {}
    if q or cat_filter or tag_filter:
        qs = SearchQuerySet()
        qs = qs.filter(content=q)
        qs = qs.filter_or(speakers__startswith=q.lower())

        if cat_filter:
            # TODO: This doesn't work quite right. It should filter
            # out anything that's not *exactly* cat_filter but it's
            # not. Could be a problem here or with the indexing. The
            # haystack docs are mysterious.
            qs = qs.filter_and(category__exact=cat_filter)
        if tag_filter:
            qs = qs.filter_and(tags__in=[tag_filter])

        # TODO: Whoosh doesn't handle faceting, so we have to do it
        # manually. Fix this so it detects whether the haystack backend
        # supports facets and if so, uses the backend and not the db.
        cat_counts = {}
        tag_counts = {}
        for mem in qs:
            cat_counts[mem.category] = cat_counts.get(mem.category, 0) + 1
            for tag in mem.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        facet_counts['category'] = sorted(
            cat_counts.items(), key=lambda pair: pair[1], reverse=True)
        facet_counts['tag'] = sorted(
            tag_counts.items(), key=lambda pair: pair[1], reverse=True)

        page = Paginator(qs, 25)
        p = request.GET.get('p', '1')
        try:
            p = max(1, int(p))
        except ValueError:
            p = 1

        try:
            page = page.page(p)
        except EmptyPage:
            page = page.page(1)
    else:
        page = None

    return render(request,
                  'videos/search.html',
                  {'query': q,
                   'tag': tag_filter,
                   'category': cat_filter,
                   'facet_counts': facet_counts,
                   'page': page})
