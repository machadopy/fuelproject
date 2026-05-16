from math import ceil
from django.core.paginator import Paginator

def make_pagination(page_range, page_current, page_qty):
    
    
    middle_page= ceil(page_qty / 2)
    fp_visual = page_current - middle_page
    lp_visual =  page_current + middle_page
    total_pages = len(page_range)

    if page_qty > total_pages:
        page_qty = total_pages


    fp_visual_offset = abs(fp_visual)
    if fp_visual < 0:
        fp_visual = 0
        lp_visual += fp_visual_offset

    if page_current > (total_pages - middle_page):
        lp_visual = total_pages
        fp_visual = lp_visual - page_qty
    
    
    pagination = page_range[fp_visual:lp_visual]
    return {
        'pagination':pagination,
        'page_range':page_range,
        'page_current':page_current,
        'page_qty':page_qty,
        'middle_page':middle_page,
        'fp_visual':fp_visual,
        'lp_visual':lp_visual,
        'total_pages':total_pages,
        'fp_visual_offset':fp_visual_offset,
        'first_page_oor': page_current > middle_page,
        'last_page_oor': lp_visual < total_pages,

    }

def make_pagination_function(request,queryset, per_page, qty_pages=4):

    page_current = request.GET.get('page') or 1
    page_current = int(page_current)

    paginator = Paginator(queryset, per_page)
    page_solicitacoes = paginator.get_page(page_current)

    pagination_range = make_pagination(
        paginator.page_range,
        page_current,
        qty_pages,
        )

    return page_solicitacoes, pagination_range