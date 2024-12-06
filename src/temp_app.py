from db.planting_area_crud import create_planting_area, get_all_planting_areas

if __name__ == "__main__":
    # Test the functions
    new_area = create_planting_area(
        area_name="Sector C",
        size_hectares=5.0,
        crop="Wheat",
        planting_date="2024-03-01",
    )
    print(f"New planting area created: {new_area}")

    areas = get_all_planting_areas()
    print(f"All planting areas: {areas}")