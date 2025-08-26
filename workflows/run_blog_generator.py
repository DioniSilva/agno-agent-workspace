#!/usr/bin/env python
import sys
from blog_post_generator import get_blog_post_generator
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Uso: python run_blog_generator.py <tópico>")
        sys.exit(1)
    
    topic = sys.argv[1]
    generator = get_blog_post_generator(debug_mode=True)
    
    print(f"Gerando blog post sobre: {topic}")
    for response in generator.run(topic=topic):
        print(f"Resposta: {response}")
