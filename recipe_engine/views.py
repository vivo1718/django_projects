from django.shortcuts import render,get_object_or_404
from .models import Recipe, Ingredient

def recipe_search_view(request):
    query = request.GET.get('ingredients', '')
    matched_recipes = []
    
    if query:
        # Convert comma-separated input (e.g. "egg, cheese ") into a clean Python list: ['egg', 'cheese']
        user_ingredients = [i.strip().lower() for i in query.split(',') if i.strip()]
        
        # Fetch all recipes from the database
        all_recipes = Recipe.objects.prefetch_related('ingredients').all()
        
        for recipe in all_recipes:
            # Gather all ingredient names required for this recipe
            recipe_ing_names = [ing.name.lower() for ing in recipe.ingredients.all()]
            
            # Find which ingredients the user HAS and what they are MISSING
            have = [ing for ing in recipe_ing_names if ing in user_ingredients]
            missing = [ing for ing in recipe_ing_names if ing not in user_ingredients]
            
            # Match condition: If the user has at least ONE ingredient for this recipe
            if have:
                # Calculate match percentage score
                match_score = (len(have) / len(recipe_ing_names)) * 100
                
                matched_recipes.append({
                    'object': recipe,
                    'have': have,
                    'missing': missing,
                    'score': round(match_score),
                    'can_make': len(missing) == 0  # True if they have everything!
                })
        
        # Sort results: Put recipes they can fully make first, then sort by highest match score
        matched_recipes.sort(key=lambda x: (x['can_make'], x['score']), reverse=True)

    return render(request, 'recipe_engine/search.html', {
        'recipes': matched_recipes,
        'query': query
    })
    
    
def recipe_detail_view(request, recipe_id):
    """Renders an interactive culinary preparation view for a targeted item."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    # Process string workflow text lines into a clean array list structure
    # Splits sentences by dots and cleans trailing white spaces
    steps = [step.strip() + "." for step in recipe.instructions.split('.') if step.strip()]
    
    return render(request, 'recipe_engine/detail.html', {
        'recipe': recipe,
        'steps': steps
    })
