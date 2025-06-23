from django.core.management.base import BaseCommand
from django.utils.text import slugify
from articles.models import Article
from sites.models import Site
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Generate test articles for development and testing"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of articles to generate per site (default: 10)'
        )
        parser.add_argument(
            '--status',
            type=str,
            choices=['pending', 'approved', 'rejected', 'mixed'],
            default='mixed',
            help='Status for generated articles (default: mixed)'
        )

    def handle(self, *args, **options):
        count = options['count']
        status_choice = options['status']
        
        # Get all sites
        sites = Site.objects.all()
        if not sites.exists():
            self.stdout.write(self.style.ERROR("No sites found. Please run 'python3 manage.py sync_sites' first."))
            return
        
        self.stdout.write(f"Generating {count} articles per site...")
        
        # Sample content for different sites
        ai_skills_content = [
            {
                "title": "The Future of AI in Software Development",
                "body": "Artificial Intelligence is revolutionizing how we write code. From GitHub Copilot to advanced debugging tools, AI assistants are becoming indispensable for developers. This article explores the latest trends in AI-powered development tools and how they're changing the industry landscape.",
                "sources": ["https://github.blog/2023-01-01/ai-coding-assistants/", "https://techcrunch.com/2023/ai-development-tools/"]
            },
            {
                "title": "Machine Learning for Beginners: Getting Started",
                "body": "Machine learning can seem intimidating, but it doesn't have to be. This comprehensive guide walks you through the fundamentals of ML, from basic concepts to your first model. We'll cover the essential tools, libraries, and resources you need to begin your ML journey.",
                "sources": ["https://scikit-learn.org/stable/getting_started.html", "https://www.tensorflow.org/tutorials"]
            },
            {
                "title": "The Rise of Prompt Engineering",
                "body": "As AI models become more sophisticated, the ability to craft effective prompts has emerged as a crucial skill. Prompt engineering is the art of communicating with AI systems to get the best possible results. Learn the techniques and best practices that can make you more effective at working with AI.",
                "sources": ["https://openai.com/blog/prompt-engineering/", "https://www.anthropic.com/prompting"]
            },
            {
                "title": "AI Ethics: Building Responsible Technology",
                "body": "With great power comes great responsibility. As AI systems become more capable, we must consider the ethical implications of our work. This article discusses bias, transparency, accountability, and other critical issues in AI development.",
                "sources": ["https://ai.google/responsibility/", "https://www.microsoft.com/en-us/ai/responsible-ai"]
            },
            {
                "title": "Natural Language Processing: Understanding Human Language",
                "body": "NLP is one of the most exciting areas of AI, enabling computers to understand and generate human language. From chatbots to translation services, NLP is transforming how we interact with technology. Explore the key concepts and applications.",
                "sources": ["https://huggingface.co/transformers/", "https://spacy.io/usage"]
            }
        ]
        
        green_living_content = [
            {
                "title": "Sustainable Home Energy: Solar Panel Installation Guide",
                "body": "Solar energy is one of the most accessible ways to make your home more sustainable. This comprehensive guide covers everything from choosing the right panels to installation and maintenance. Learn how to reduce your carbon footprint while saving money on energy bills.",
                "sources": ["https://www.energy.gov/eere/solar/homeowners-guide-going-solar", "https://www.solarreviews.com/"]
            },
            {
                "title": "Zero-Waste Kitchen: Practical Tips for Beginners",
                "body": "Reducing kitchen waste doesn't have to be overwhelming. Start with these simple, practical tips that anyone can implement. From composting to smart shopping, discover how small changes can make a big environmental impact.",
                "sources": ["https://www.epa.gov/recycle/reducing-wasted-food-home", "https://www.zerowastehome.com/"]
            },
            {
                "title": "Eco-Friendly Transportation: Beyond Electric Cars",
                "body": "While electric vehicles get most of the attention, there are many other sustainable transportation options. From bicycles to public transit, carpooling to walking, explore the full spectrum of green transportation choices available to you.",
                "sources": ["https://www.transit.dot.gov/", "https://www.bikeleague.org/"]
            },
            {
                "title": "Sustainable Fashion: Building a Conscious Wardrobe",
                "body": "Fast fashion is one of the biggest environmental polluters. Learn how to build a sustainable wardrobe that's both stylish and eco-friendly. From choosing sustainable materials to supporting ethical brands, make fashion choices that align with your values.",
                "sources": ["https://www.greenpeace.org/international/story/29176/fast-fashion-dirty-secret/", "https://www.goodonyou.eco/"]
            },
            {
                "title": "Urban Gardening: Growing Food in Small Spaces",
                "body": "You don't need a large backyard to grow your own food. Urban gardening techniques like container gardening, vertical farming, and community gardens make it possible to grow fresh produce in even the smallest spaces. Start your urban farming journey today.",
                "sources": ["https://www.urbanfarm.org/", "https://www.gardeners.com/"]
            }
        ]
        
        # Content mapping for each site
        site_content = {
            'ai-skills': ai_skills_content,
            'green-living': green_living_content
        }
        
        articles_created = 0
        
        for site in sites:
            self.stdout.write(f"Generating articles for site: {site.name}")
            
            # Get content for this site
            content_list = site_content.get(site.slug, ai_skills_content)  # Default to AI content
            
            for i in range(count):
                # Select content (cycle through available content)
                content = content_list[i % len(content_list)]
                
                # Determine status
                if status_choice == 'mixed':
                    status = random.choice(['pending', 'approved', 'rejected'])
                else:
                    status = status_choice
                
                # Create unique title and slug
                title = f"{content['title']} - Part {i+1}"
                # Create a shorter slug from the base title (before "Part X")
                base_title = content['title']
                slug = slugify(base_title)[:50]  # Limit to 50 chars
                
                # Ensure unique slug
                counter = 1
                original_slug = slug
                while Article.objects.filter(slug=slug).exists():
                    slug = f"{original_slug[:40]}-{counter}"  # Keep under 50 chars
                    counter += 1
                
                # Create article
                article = Article.objects.create(
                    site=site,
                    title=title,
                    slug=slug,
                    body=content['body'],
                    sources=content['sources'],
                    status=status,
                    created_at=datetime.now() - timedelta(days=random.randint(0, 30))
                )
                
                articles_created += 1
                self.stdout.write(f"  Created: {title} ({status})")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {articles_created} test articles across {sites.count()} sites!"
            )
        )
        
        # Summary by status
        for status in ['pending', 'approved', 'rejected']:
            count = Article.objects.filter(status=status).count()
            self.stdout.write(f"  {status.capitalize()}: {count} articles") 