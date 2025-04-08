from django.test import TestCase
from django.urls import reverse
from  .views import getVids, getImg, getArt

# Create your tests here.
class ResourcesTestCase(TestCase):
    def testGetVids(self):
        print("Videos")
        vids = getVids()
        self.assertEqual(len(vids), 10)
        self.assertTrue(any("youtube"in v.link.lower() for v in vids))

    def testGetArt(self):
        art = getArt()
        self.assertEqual(len(art), 8)
        self.assertTrue(all(a.link.startswith("https://") for a in art))

    def testGetImg(self):
        img = getImg()
        self.assertEqual(len(img), 4)
        self.assertTrue(all(i.link.startswith("https://") for i in img))