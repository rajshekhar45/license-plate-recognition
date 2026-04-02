def detect_plate(image_path):
    try:
        from license_plate_extraction import extract_plate

        plate_number = extract_plate(image_path)

        if plate_number:
            return plate_number
        else:
            return "No plate detected❌"

    except Exception as e:
        return f"Error: {str(e)}"