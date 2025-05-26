"""Script to run migrations on a shared hosting server (Namecheap)"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.system("alembic upgrade head")
