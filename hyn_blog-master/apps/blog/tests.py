from django.test import TestCase

# Create your tests here.
from django.contrib.auth.hashers import make_password, check_password

p1 = "ceshi1"
p2 = make_password(p1)
print(p2)
leg = check_password(p1, p2)
print(leg)