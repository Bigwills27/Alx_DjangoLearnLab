from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Comment, Category, Like
import random


class Command(BaseCommand):
    help = 'Create sample data for the blog'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Technology', 'slug': 'technology', 'description': 'All about tech trends and innovations'},
            {'name': 'Lifestyle', 'slug': 'lifestyle', 'description': 'Living life to the fullest'},
            {'name': 'Travel', 'slug': 'travel', 'description': 'Exploring the world'},
            {'name': 'Food', 'slug': 'food', 'description': 'Culinary adventures and recipes'},
            {'name': 'Health', 'slug': 'health', 'description': 'Health and wellness tips'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")

        # Create test users if they don't exist
        if not User.objects.filter(username='blogger1').exists():
            user1 = User.objects.create_user(
                username='blogger1',
                email='blogger1@example.com',
                password='testpass123',
                first_name='Alice',
                last_name='Johnson'
            )
            self.stdout.write("Created user: blogger1")
        else:
            user1 = User.objects.get(username='blogger1')

        if not User.objects.filter(username='blogger2').exists():
            user2 = User.objects.create_user(
                username='blogger2',
                email='blogger2@example.com',
                password='testpass123',
                first_name='Bob',
                last_name='Smith'
            )
            self.stdout.write("Created user: blogger2")
        else:
            user2 = User.objects.get(username='blogger2')

        # Sample posts data
        sample_posts = [
            {
                'title': 'The Future of Artificial Intelligence',
                'content': '''Artificial Intelligence is revolutionizing how we interact with technology. From machine learning algorithms that can predict user behavior to natural language processing systems that can understand and respond to human queries, AI is becoming an integral part of our daily lives.

In this post, we'll explore the current state of AI technology and discuss what the future might hold. We'll look at emerging trends like autonomous vehicles, smart home systems, and AI-powered healthcare solutions.

The potential applications are endless, and the pace of innovation shows no signs of slowing down. As we move forward, it's important to consider both the opportunities and challenges that AI presents.''',
                'author': user1,
                'category': 'technology',
                'tags': ['AI', 'technology', 'future', 'machine learning'],
                'is_featured': True
            },
            {
                'title': 'Finding Balance in a Digital World',
                'content': '''In our increasingly connected world, finding balance between digital engagement and real-world experiences has become more important than ever. This post explores practical strategies for maintaining mental health and personal relationships in the digital age.

We'll discuss digital detox techniques, mindful technology use, and ways to create boundaries between online and offline life. The goal isn't to eliminate technology, but to use it intentionally and purposefully.

Remember, technology should enhance our lives, not control them. Let's explore how to make that a reality.''',
                'author': user2,
                'category': 'lifestyle',
                'tags': ['lifestyle', 'digital wellness', 'balance', 'mindfulness'],
                'is_featured': False
            },
            {
                'title': 'Hidden Gems: Off the Beaten Path Destinations',
                'content': '''Traveling doesn't always mean visiting the most popular tourist destinations. Some of the most memorable experiences come from discovering hidden gems that few people know about.

In this guide, we'll share some incredible off-the-beaten-path destinations that offer unique experiences, stunning natural beauty, and authentic cultural encounters. From remote islands to mountain villages, these places offer something special for the adventurous traveler.

Pack your bags and prepare for an adventure unlike any other!''',
                'author': user1,
                'category': 'travel',
                'tags': ['travel', 'adventure', 'hidden gems', 'exploration'],
                'is_featured': False
            },
            {
                'title': 'Farm-to-Table: The Art of Seasonal Cooking',
                'content': '''There's something magical about cooking with ingredients that are in season and sourced locally. Farm-to-table cooking not only tastes better but also supports local communities and reduces environmental impact.

In this post, we'll explore the benefits of seasonal cooking and share some delicious recipes that highlight the best of each season. We'll also discuss how to find local farmers' markets and build relationships with local producers.

Get ready to transform your cooking and discover flavors you never knew existed!''',
                'author': user2,
                'category': 'food',
                'tags': ['cooking', 'farm-to-table', 'seasonal', 'local food'],
                'is_featured': False
            },
            {
                'title': 'The Science of Sleep: Optimizing Your Rest',
                'content': '''Quality sleep is one of the most important factors for overall health and well-being. Yet many people struggle with sleep issues that affect their daily lives and long-term health.

This comprehensive guide explores the science behind sleep, including sleep cycles, the importance of REM sleep, and how various factors affect sleep quality. We'll also share practical tips for improving your sleep hygiene and creating the ideal sleep environment.

Transform your nights and wake up feeling refreshed and energized!''',
                'author': user1,
                'category': 'health',
                'tags': ['health', 'sleep', 'wellness', 'science'],
                'is_featured': False
            }
        ]

        # Create posts
        for post_data in sample_posts:
            category = Category.objects.get(slug=post_data['category'])
            
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'content': post_data['content'],
                    'author': post_data['author'],
                    'category': category,
                    'is_featured': post_data['is_featured']
                }
            )
            
            if created:
                # Add tags
                for tag_name in post_data['tags']:
                    post.tags.add(tag_name)
                
                self.stdout.write(f"Created post: {post.title}")

        # Create some sample comments
        posts = Post.objects.all()
        users = [user1, user2]
        
        sample_comments = [
            "Great post! Really enjoyed reading this.",
            "Thanks for sharing this valuable information.",
            "This is exactly what I was looking for.",
            "Excellent insights. Looking forward to more content like this.",
            "Very well written and informative.",
            "I learned something new today. Thank you!",
            "Amazing content as always!",
            "This gave me a new perspective on the topic."
        ]

        for post in posts:
            # Add 2-4 random comments per post
            num_comments = random.randint(2, 4)
            for _ in range(num_comments):
                Comment.objects.get_or_create(
                    post=post,
                    author=random.choice(users),
                    content=random.choice(sample_comments)
                )

        # Create some likes
        for post in posts:
            # Each user likes 2-3 random posts
            for user in users:
                if random.choice([True, False, False]):  # 33% chance
                    Like.objects.get_or_create(user=user, post=post)

        self.stdout.write(self.style.SUCCESS('Successfully created sample data!'))
