from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from core.forms import VoteForm
from core.models import Movie, Person, Vote

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView

from core.forms import MovieImageForm


class MovieList(ListView):
    paginate_by = 10  # 分页，一页20个
    ordering = '-title'  # 排序
    model = Movie


class PersonList(ListView):
    model = Person


class MovieDetail(DetailView):
    queryset = Movie.objects.all_with_related_persons_and_score()

    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_form'] = self.movie_image_form()
        if self.request.user.is_authenticated:
            #  这边看
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user
            )
            #  如果存在投票记录,和如果不存在投票记录，
            #  通过vote_form_url 决定，是要更新还是新投票
            #  这里，我也可以预判，这题做没做，如果做过就更新，如果没做就
            #  新做
            if vote.id:
                vote_form_url = reverse('core:UpdateVote',
                                        kwargs={'movie_id': vote.movie.id,
                                                'pk': vote.id})
            else:
                vote_form_url = reverse('core:CreateVote',
                                        kwargs={
                                            'movie_id': self.object.id
                                        })
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
            print(ctx)
        return ctx


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('cannot change another users vote')
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)


class MovieImageUpload(LoginRequiredMixin, CreateView):
    form_class = MovieImageForm

    #  初始化表格
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return movie_detail_url
