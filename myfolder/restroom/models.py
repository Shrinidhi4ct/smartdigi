from django.db import models

# Create your models here.
class RestroomReasonSetup(models.Model):
    """
    Model to store restroom reasons
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    display_text = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    display_image = models.ImageField(upload_to="static/reasons/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reason_setup"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


# Floor Setup
class FloorSetup(models.Model):
    """
    Model to store floor setup
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    floor_map = models.ImageField(upload_to="static/floors/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "floor_setup"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


# Room setup
class RoomSetup(models.Model):
    """
    Model to store room setup
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    floor = models.ForeignKey(
        FloorSetup, on_delete=models.CASCADE, related_name="rooms"
    )
    room_shape = models.CharField(max_length=100, blank=True, null=True)
    room_location = models.TextField(blank=True, null=True)
    room_idenfier = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "room_setup"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class CheckListSetup(models.Model):
    """
    Model to store checklist items
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    display_text = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    display_image = models.ImageField(upload_to="static/checklist/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "checklist_setup"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Tickets(models.Model):
    """
    Model to store tickets
    """

    id = models.AutoField(primary_key=True, editable=False)
    reason = models.JSONField()
    feedback = models.BooleanField(default=False)
    room = models.ForeignKey(
        RoomSetup,
        on_delete=models.CASCADE,
        related_name="tickets_room",
        null=True,
        blank=True,
    )
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="ticket_update",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "tickets"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)


class CheckList(models.Model):
    """
    Model to store checklist
    """

    id = models.AutoField(primary_key=True, editable=False)
    checklist = models.JSONField()
    room = models.ForeignKey(
        RoomSetup,
        on_delete=models.CASCADE,
        related_name="checklist_room",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="checklist"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "checklist"
        ordering = ["-created_at"]

    def __str__(self):
        return self.id


class RatingSetup(models.Model):
    """
    Model to store rating setup
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    positive_image = models.ImageField(
        upload_to="static/rating/", blank=True, null=True
    )
    negative_image = models.ImageField(
        upload_to="static/rating/", blank=True, null=True
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rating_setup"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class AlertConditions(models.Model):
    """
        model to store alert conditions
    """
    
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    email = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "alert_conditions"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Alert_history(models.Model):
    """
    Model to store alerts history
    """
    
    id = models.AutoField(primary_key=True, editable=False)
    parameter = models.CharField(max_length=100, blank=True, null=True)
    is_email_sent = models.BooleanField(default=False)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "alert_history"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)