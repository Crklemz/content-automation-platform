from django.core.management.base import BaseCommand
from sites.models import Site
import json
from pathlib import Path


class Command(BaseCommand):
    help = "Sync sites from root-level data/site_config.json into the Site model"

    def handle(self, *args, **kwargs):
        backend_dir = Path(__file__).resolve().parents[3]
        config_path = backend_dir.parent / "data" / "site_config.json"

        if not config_path.exists():
            self.stderr.write(self.style.ERROR(f"Config file not found: {config_path}"))
            return

        with open(config_path) as f:
            try:
                site_data = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(self.style.ERROR(f"Error parsing JSON: {e}"))
                return

        for site in site_data:
            obj, created = Site.objects.update_or_create(
                slug=site["slug"],
                defaults={
                    "name": site["name"],
                    "description": site.get("description", ""),
                    "logo": site.get("logo", ""),
                    "primary_color": site.get("primary_color", "#000000"),
                    "secondary_color": site.get("secondary_color", "#FFFFFF"),
                },
            )
            status = "Created" if created else "Updated"
            self.stdout.write(f"{status} site: {site['slug']}")

        self.stdout.write(self.style.SUCCESS("Site sync complete."))
