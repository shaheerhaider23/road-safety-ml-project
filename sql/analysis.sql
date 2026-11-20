SELECT road_type, severity_label, COUNT(*) AS collision_count
        FROM collisions
        GROUP BY road_type, severity_label
        ORDER BY road_type, collision_count DESC;
