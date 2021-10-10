select count(distinct category.name) numCats
from category,
    (select distinct item.id, bid.amount
    from item, bid
    where bid.bid_on = item.id
    and CAST(bid.amount AS INT) > 100) items
where items.id = category.item