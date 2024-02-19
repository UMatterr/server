from django.db import models


class NLPEventModel(models.Model):

    id = models.AutoField(
        primary_key=True,
        editable=False,
        db_column='id',
    )
    event = models.ForeignKey(
        'nlp.NLPEvents',
        on_delete=models.CASCADE,
        db_column='event_id',
    )
    model = models.ForeignKey(
        'nlp.NLPModels',
        on_delete=models.CASCADE,
        db_column='model_id',
    )
    desc = models.TextField(
        null=True,
        db_column='desc',
    )

    class Meta:
        # using = 'nlp_db'
        db_table = 'event_model'


class NLPEvents(models.Model):

    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    evnet_name = models.CharField(
        max_length=32,
        db_column='event_name',
    )
    desc = models.TextField(
        null=True,
        db_column='desc',
    )

    class Meta:
        db_table = 'events'


class NLPModels(models.Model):

    model_types = [
        ('S', 'Service'),
        ('T', 'Training'),
    ]

    id = models.AutoField(
        primary_key=True,
        editable=False,
        db_column='id',
    )
    name = models.CharField(
        max_length=64,
        db_column='name',
    )
    type = models.CharField(
        max_length=1,
        db_column='type',
        choices=model_types,
    )
    path = models.CharField(
        max_length=1024,
        db_column='path',
    )
    base = models.CharField(
        max_length=1024,
        db_column='base',
    )
    version = models.CharField(
        max_length=32,
        db_column='version',
    )
    desc = models.TextField(
        null=True,
        db_column='desc',
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        db_column='last_modified',
    )
    token_base = models.CharField(
        max_length=200,
        db_column='token_base',
    )
    token_path = models.CharField(
        max_length=200,
        db_column='token_path',
    )
    train_prefix = models.CharField(
        max_length=200,
        db_column='train_prefix',
    )

    class Meta:
        db_table = 'models'


class NLPInputTexts(models.Model):

    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    event = models.ForeignKey(
        'nlp.NLPEvents',
        on_delete=models.CASCADE,
        db_column='event_id',
    )
    input_text = models.TextField(
        db_column='input_text',
    )
    desc = models.TextField(
        null=True,
        db_column='desc',
    )
    enable = models.BooleanField(
        default=False,
        db_column='enable',
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        db_column='last_modified',
    )

    class Meta:
        db_table = 'input_texts'


class NLPCacheTexts(models.Model):

    id = models.AutoField(
        primary_key=True,
        editable=False,
        db_column='id',
    )
    event = models.ForeignKey(
        'nlp.NLPEvents',
        on_delete=models.CASCADE,
        db_column='event_id',
    )
    cache_text = models.TextField(
        db_column='cache_text',
    )
    enable = models.BooleanField(
        default=False,
        db_column='enable',
    )

    class Meta:
        db_table = 'cache_texts'


class NLPTrainReservation(models.Model):

    status_types = [
        ('N', 'Not started'),
        ('S', 'Started'),
        ('P', 'Paused'),
        ('C', 'Completed'),
        ('E', 'Error'),
    ]

    id = models.AutoField(
        primary_key=True,
        editable=False,
        db_column='id',
    )
    event_model = models.ForeignKey(
        'nlp.NLPEventModel',
        on_delete=models.CASCADE,
        db_column='event_model_id',
    )
    train_data = models.ForeignKey(
        'nlp.NLPTrainData',
        on_delete=models.CASCADE,
        db_column='train_data_id',
    )
    start_time = models.DateTimeField(
        auto_now=True,
        db_column='start_time',
    )
    enable = models.BooleanField(
        default=False,
        db_column='enable',
    )
    status = models.CharField(
        max_length=1,
        choices=status_types,
        db_column='status',
    )

    class Meta:
        db_table = 'train_reservation'


class NLPTrainData(models.Model):

    id = models.AutoField(
        primary_key=True,
        editable=False,
        db_column='id',
    )
    data = models.BinaryField(
        db_column='data',
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        db_column='last_modified',
    )

    class Meta:
        db_table = 'train_data'


class NLPConfig(models.Model):

    id = models.AutoField(
        primary_key=True,
        editable=False,
        db_column='id',
    )
    key = models.CharField(
        max_length=32,
        db_column='key',
    )
    value = models.CharField(
        max_length=32,
        db_column='value',
    )

    class Meta:
        db_table = 'config'
