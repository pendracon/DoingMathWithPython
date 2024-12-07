import unittest
from conversion import km_to_miles, miles_to_km, kg_to_pounds, pounds_to_kg, celsius_to_fahrenheit, fahrenheit_to_celsius

class TestConversionFunctions(unittest.TestCase):

    def test_km_to_miles(self):
        result = km_to_miles(1)
        print(f"km_to_miles(1): {result}")
        self.assertAlmostEqual(result, 0.621371)
        self.assertAlmostEqual(km_to_miles(0), 0)
        self.assertAlmostEqual(km_to_miles(10), 6.21371)
        self.assertNotAlmostEqual(km_to_miles(1), 1)  # Failure condition

    def test_miles_to_km(self):
        result = miles_to_km(1)
        print(f"miles_to_km(1): {result}")
        self.assertAlmostEqual(result, 1.60934)
        self.assertAlmostEqual(miles_to_km(0), 0)
        self.assertAlmostEqual(miles_to_km(10), 16.0934)
        self.assertNotAlmostEqual(miles_to_km(1), 2)  # Failure condition

    def test_kg_to_pounds(self):
        result = kg_to_pounds(1)
        print(f"kg_to_pounds(1): {result}")
        self.assertAlmostEqual(result, 2.20462)
        self.assertAlmostEqual(kg_to_pounds(0), 0)
        self.assertAlmostEqual(kg_to_pounds(10), 22.0462)
        self.assertNotAlmostEqual(kg_to_pounds(1), 3)  # Failure condition

    def test_pounds_to_kg(self):
        result = pounds_to_kg(1)
        print(f"pounds_to_kg(1): {result}")
        self.assertAlmostEqual(result, 0.453592)
        self.assertAlmostEqual(pounds_to_kg(0), 0)
        self.assertAlmostEqual(pounds_to_kg(10), 4.53592)
        self.assertNotAlmostEqual(pounds_to_kg(1), 1)  # Failure condition

    def test_celsius_to_fahrenheit(self):
        result = celsius_to_fahrenheit(0)
        print(f"celsius_to_fahrenheit(0): {result}")
        self.assertAlmostEqual(result, 32)
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212)
        self.assertAlmostEqual(celsius_to_fahrenheit(-40), -40)
        self.assertNotAlmostEqual(celsius_to_fahrenheit(0), 0)  # Failure condition

    def test_fahrenheit_to_celsius(self):
        result = fahrenheit_to_celsius(32)
        print(f"fahrenheit_to_celsius(32): {result}")
        self.assertAlmostEqual(result, 0)
        self.assertAlmostEqual(fahrenheit_to_celsius(212), 100)
        self.assertAlmostEqual(fahrenheit_to_celsius(-40), -40)
        self.assertNotAlmostEqual(fahrenheit_to_celsius(32), 32)  # Failure condition

if __name__ == '__main__':
    unittest.main()