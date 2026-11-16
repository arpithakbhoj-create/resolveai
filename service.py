
from datetime import datetime, timezone

from models import IncidentUpdate

from models import (
    Incident,
    IncidentCreate,
    IncidentStatus
)

from database import get_db_connection


# CREATE INCIDENT
def create_incident_service(incident_data: IncidentCreate):

    connection = get_db_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO incidents (
                title,
                description,
                category,
                priority,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                incident_data.title,
                incident_data.description,
                incident_data.category.value,
                incident_data.priority.value,
                IncidentStatus.OPEN.value
            )
        )

        connection.commit()

        incident_id = cursor.lastrowid

        return get_incident_by_id_service(incident_id)

    finally:
        connection.close()


# GET ALL INCIDENTS
def get_incidents_service():

    connection = get_db_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM incidents ORDER BY id DESC"
        ).fetchall()

        return [
            Incident(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                category=row["category"],
                priority=row["priority"],
                status=row["status"],
                resolution_notes=row["resolution_notes"],
                resolved_at=row["resolved_at"]
            )
            for row in rows
        ]

    finally:
        connection.close()


# GET INCIDENT BY ID
def get_incident_by_id_service(incident_id: int):

    connection = get_db_connection()

    try:
        row = connection.execute(
            "SELECT * FROM incidents WHERE id = ?",
            (incident_id,)
        ).fetchone()

        if row is None:
            return None

        
        return Incident(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        category=row["category"],
        priority=row["priority"],
        status=row["status"],
        resolution_notes=row["resolution_notes"],
        resolved_at=row["resolved_at"]
)


    finally:
        connection.close()

    
# UPDATE INCIDENT
def update_incident_service(
    incident_id: int,
    incident_data: IncidentUpdate
):

    # Check whether the incident exists
    existing_incident = get_incident_by_id_service(incident_id)

    if existing_incident is None:
        return None

    # Get only fields provided in the request
    updates = incident_data.model_dump(exclude_unset=True)

    # Do not allow explicit null values
    if any(value is None for value in updates.values()):
        raise ValueError("Incident fields cannot be null")

    # Convert Enum values into database strings
    for field in ("category", "priority", "status"):
        if field in updates:
            updates[field] = updates[field].value

    # Determine the resulting incident status
    new_status = updates.get(
        "status",
        existing_incident.status.value
    )

    # Determine the resulting resolution notes
    new_notes = updates.get(
        "resolution_notes",
        existing_incident.resolution_notes
    )

    # Apply resolution rules
    if new_status == IncidentStatus.RESOLVED.value:

        if not new_notes or not new_notes.strip():
            raise ValueError(
                "Resolution notes are required to resolve an incident"
            )

        if existing_incident.status != IncidentStatus.RESOLVED:
            updates["resolved_at"] = datetime.now(
                timezone.utc
            ).isoformat()

    elif "status" in updates:
        # Clear the resolution timestamp if reopened
        updates["resolved_at"] = None

    # Nothing to update
    if not updates:
        return existing_incident

    # Build a parameterized SQL UPDATE statement
    columns = ", ".join(
        f"{field} = ?" for field in updates
    )

    values = list(updates.values())
    values.append(incident_id)

    
    connection = get_db_connection()

    try:
        # Read existing database values before updating
        current_row = connection.execute(
            "SELECT * FROM incidents WHERE id = ?",
            (incident_id,)
        ).fetchone()

        if current_row is None:
            return None

        # Record the time of this update
        changed_at = datetime.now(
            timezone.utc
        ).isoformat()

        # Compare old and new values
        for field, new_value in updates.items():

            old_value = current_row[field]

            # Record history only if the value changed
            if old_value != new_value:
                connection.execute(
                    """
                    INSERT INTO incident_history (
                        incident_id,
                        field_name,
                        old_value,
                        new_value,
                        changed_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        incident_id,
                        field,
                        old_value,
                        new_value,
                        changed_at
                    )
                )

        # Update the incident record
        connection.execute(
            f"UPDATE incidents SET {columns} WHERE id = ?",
            values
        )

        # Save incident changes and history together
        connection.commit()

    finally:
        connection.close()

    return get_incident_by_id_service(incident_id)


# GET INCIDENT HISTORY
def get_incident_history_service(incident_id: int):

    connection = get_db_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                incident_id,
                field_name,
                old_value,
                new_value,
                changed_at
            FROM incident_history
            WHERE incident_id = ?
            ORDER BY changed_at ASC, id ASC
            """,
            (incident_id,)
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


# GET INCIDENT STATISTICS
def get_incident_statistics_service():

    connection = get_db_connection()

    try:
        # Total incidents
        total_incidents = connection.execute(
            "SELECT COUNT(*) FROM incidents"
        ).fetchone()[0]

        # Count incidents by status
        status_rows = connection.execute(
            """
            SELECT status, COUNT(*) AS count
            FROM incidents
            GROUP BY status
            """
        ).fetchall()

        status_counts = {
            row["status"]: row["count"]
            for row in status_rows
        }

        # Count incidents by priority
        priority_rows = connection.execute(
            """
            SELECT priority, COUNT(*) AS count
            FROM incidents
            GROUP BY priority
            """
        ).fetchall()

        priority_counts = {
            row["priority"]: row["count"]
            for row in priority_rows
        }

        # Count incidents by category
        category_rows = connection.execute(
            """
            SELECT category, COUNT(*) AS count
            FROM incidents
            GROUP BY category
            """
        ).fetchall()

        category_counts = {
            row["category"]: row["count"]
            for row in category_rows
        }

        # Calculate average resolution time in hours
        average_resolution = connection.execute(
            """
            SELECT AVG(
                (julianday(resolved_at) -
                 julianday(created_at)) * 24
            )
            FROM incidents
            WHERE resolved_at IS NOT NULL
            """
        ).fetchone()[0]

        return {
            "total_incidents": total_incidents,
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "category_counts": category_counts,
            "average_resolution_hours": (
                round(average_resolution, 2)
                if average_resolution is not None
                else None
            )
        }

    finally:
        connection.close()

    

# GET RESOLVED INCIDENTS WITH RESOLUTION NOTES
def get_resolved_incidents_service():

    connection = get_db_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                title,
                description,
                category,
                priority,
                status,
                resolution_notes,
                resolved_at
            FROM incidents
            WHERE status = 'Resolved'
              AND resolution_notes IS NOT NULL
              AND TRIM(resolution_notes) != ''
            ORDER BY resolved_at DESC
            """
        ).fetchall()

        return [
            Incident(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                category=row["category"],
                priority=row["priority"],
                status=row["status"],
                resolution_notes=row["resolution_notes"],
                resolved_at=row["resolved_at"]
            )
            for row in rows
        ]

    finally:
        connection.close()
