# Generated by Django 4.0.1 on 2022-11-20 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_evaluationsubmission_assignments_feedback_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='assignments_feedback',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='assignments_guidance',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='assignments_promptitude',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='assignments_relevance',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='attendance_presence',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='attendance_punctuality',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='attendance_schedule',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='curriculum_feedback_beginning_answer',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='curriculum_feedback_books_answer',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='curriculum_feedback_course_answer',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='curriculum_feedback_lecture_answer',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='curriculum_feedback_outcomes_answer',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='curriculum_feedback_procedures_answer',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_achievements',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_clarity',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_contents',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_enthusiasm',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_innovation',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_organization',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_responsiveness',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_sequence',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='delivery_theory_practices',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_air_conditioning',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_audio_visual_equip',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_books',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_classroom_size',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_computers',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_internet',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_public_address',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_seats',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='environment_secretariat',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='interaction_availability',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='interaction_fairness',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
        migrations.AlterField(
            model_name='evaluationsubmission',
            name='interaction_help',
            field=models.IntegerField(choices=[(0, 'Not Applicable'), (1, 'Strongly Disagree'), (2, 'Disagree'), (3, 'Moderately Disagree'), (4, 'Agree'), (5, 'Strongly Agree')], default=None),
        ),
    ]