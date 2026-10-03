from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from apps.calendar_tasks.models import CalendarTask, CalendarFeedToken
from apps.calendar_tasks.services.ical_exporter import generate_ical_feed


class CalendarTasksTestCase(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        self.task = CalendarTask.objects.create(
            title="Review Vendor Contract",
            task_type=CalendarTask.TaskType.CONTRACT_RENEWAL,
            due_date=self.today + timedelta(days=5),
            priority=CalendarTask.Priority.HIGH,
            status=CalendarTask.Status.PENDING
        )

    def test_ical_feed_generation(self):
        feed_bytes = generate_ical_feed()
        feed_text = feed_bytes.decode('utf-8')

        self.assertIn("BEGIN:VCALENDAR", feed_text)
        self.assertIn("Review Vendor Contract", feed_text)
        self.assertIn("END:VCALENDAR", feed_text)

    def test_ical_endpoint(self):
        token = CalendarFeedToken.objects.create(name="Test Feed")
        response = self.client.get(f"/calendar/feed.ics?token={token.token}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/calendar", response['Content-Type'])
        self.assertIn("Review Vendor Contract", response.content.decode('utf-8'))

    def test_calendar_events_api(self):
        response = self.client.get("/calendar/api/events/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) >= 1)
        self.assertIn("Review Vendor Contract", data[0]['title'])
