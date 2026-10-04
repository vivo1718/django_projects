from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice

def poll_view(request):
    # Fetch the very first question from the database
    question = Question.objects.first()
    
    # NEXT-LEVEL: Session check! If they already voted, send them straight to results
    if request.session.get(f'has_voted_{question.id}', False):
        return redirect('vote_results', question_id=question.id)
        
    return render(request, 'polls/vote.html', {'question': question})

def vote_submit(request):
    question = Question.objects.first()
    
    if request.method == 'POST':
        # Double check sessions on submission to prevent cheating
        if request.session.get(f'has_voted_{question.id}', False):
            return redirect('vote_results', question_id=question.id)
            
        choice_id = request.POST.get('choice')
        if choice_id:
            # Fetch the selected choice safely and increment its vote count
            selected_choice = get_object_or_404(Choice, pk=choice_id, question=question)
            selected_choice.votes += 1
            selected_choice.save()
            
            # NEXT-LEVEL: Mark this specific browser session as "voted"
            request.session[f'has_voted_{question.id}'] = True
            
            return redirect('vote_results', question_id=question.id)
            
    return redirect('poll_view')

def vote_results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    
    total_votes = sum(c.votes for c in choices)
    
    results = []
    for c in choices:
        percentage = (c.votes / total_votes * 100) if total_votes > 0 else 0
        results.append({
            'text': c.choice_text,
            'votes': c.votes,
            'percentage': round(percentage, 1)
        })
        
    return render(request, 'polls/results.html', {
        'question': question.question_text,
        'results': results,
        'total_votes': total_votes
    })
