# seed.py
from datetime import datetime
from app import app, db, Hero, Power, HeroPower

def seed_data():
    with app.app_context():
        # Clear existing data
        print("Clear existing data...")
        HeroPower.query.delete()
        Hero.query.delete()
        Power.query.delete()
        db.session.commit()
        #populate new data
        print("🦸‍♀️ Seeding powers...")
        powers_data = [
            {"name": "super strength", "description": "gives the wielder super-human strengths"},
            {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
            {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
            {"name": "elasticity", "description": "can stretch the human body to extreme lengths"},
        ]
        powers = [Power(**data) for data in powers_data]
        db.session.add_all(powers)
        db.session.commit()

        print("🦸‍♀️ Seeding heroes...")
        heroes_data = [
            {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
            {"name": "Doreen Green", "super_name": "Squirrel Girl"},
            {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
            {"name": "Janet Van Dyne", "super_name": "The Wasp"},
            {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
            {"name": "Carol Danvers", "super_name": "Captain Marvel"},
            {"name": "Jean Grey", "super_name": "Dark Phoenix"},
            {"name": "Ororo Munroe", "super_name": "Storm"},
            {"name": "Kitty Pryde", "super_name": "Shadowcat"},
            {"name": "Elektra Natchios", "super_name": "Elektra"},
        ]
        heroes = [Hero(**data) for data in heroes_data]
        db.session.add_all(heroes)
        db.session.commit()

        print("🦸‍♀️ Adding powers to heroes...")
        strengths = ["Strong", "Weak", "Average"]
        for hero in Hero.query.all():
            for _ in range(1, 4):  # Adjust the range as needed
                power = Power.query.order_by(db.func.random()).first()
                
                # Check if strengths list is empty and refill it if needed
                if not strengths:
                    strengths = ["Strong", "Weak", "Average"]

                hero_power = HeroPower(hero=hero, power=power, strength=strengths.pop())
                db.session.add(hero_power)
        db.session.commit()

        print("🦸‍♀️ Done seeding!")

if __name__ == "__main__":
    seed_data()
