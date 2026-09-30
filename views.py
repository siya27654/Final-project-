from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, Submission


def submit(request):
    if request.method == "POST":
        submission = Submission.objects.create()

        for question in Question.objects.all():
            choice_id = request.POST.get(f"question_{question.id}")
            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id)
                submission.choices.add(choice)

        return redirect("show_exam_result", submission_id=submission.id)

    questions = Question.objects.all()
    return render(request, "exam.html", {"questions": questions})


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    score = 0
    total = Question.objects.count()

    for question in Question.objects.all():
        selected_choice = submission.choices.filter(question=question).first()
        if selected_choice and selected_choice.is_correct:
            score += 1

    return render(
        request,
        "exam_result.html",
        {
            "submission": submission,
            "score": score,
            "total": total,
        },
    )
