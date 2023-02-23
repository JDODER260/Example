
class PostListView(NotificationMixin, FilterView):
    paginate_by = 6
    ordering = ['-date_posted']
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    filterset_class = PostFilterSet
    
    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Post.objects.filter(category='Complaints') | \
                   Post.objects.filter(category='Feature-Requests') | \
                   Post.objects.filter(category='Conversation') | \
                   Post.objects.filter(category='Coding') | \
                   Post.objects.filter(category='Implemented-requests') | \
                   Post.objects.filter(category='Questions')
        queryset = queryset.order_by('-date_posted')
        return queryset
    
    @method_decorator(csrf_exempt)
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        posts = Post.objects.all()
        
        # Get the total number of comments for each post
        lists_comm = []
        for i in posts:
            comm = 0
            for x in i.comments.all():
                comm += 1
            lists_comm.append({"post": i.title, "total_comms": comm})
        
        # Get the top 5 posts with the most likes
        hero_section = sorted(posts, key=lambda x: x.likes.count(), reverse=True)[:5]
        
        # Get the most recent 7 posts
        post_grid_section = posts.order_by('-date_posted')[:6]
        pg1 = post_grid_section[:3]
        pg2 = post_grid_section[3:6]
        # Get all the posts with the category "Chess"
        chess_category_section = posts.filter(category='Chess')
        ranone = random.choice(posts)
        
        # Get the 6 most commented posts
        trending_posts = sorted(posts, key=lambda post: post.comments.count(), reverse=True)[:6]
        
        # Get the 6 most recent posts
        latest_posts = posts.order_by('-date_posted')[:6]
        if self.request.user.is_authenticated: 
            context["popular_posts"] = hero_section
            context["trending_posts"] = trending_posts
            context["latest_posts"] = latest_posts
            context["hero_section"] = hero_section
            context["pg1"] = pg1
            context["pg2"] = pg2
            context["ranone"] = ranone
            context["post_grid_section"] = post_grid_section
            context["chess_category_section"] = chess_category_section
            context["comment_post_list"] = lists_comm
            context["hello"] = self.request.user.is_authenticated
        
        return context
