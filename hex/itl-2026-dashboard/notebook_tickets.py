# Ticket sales native tables (daily / mix / vs goal). Hex App uses one table per cell.
from ticket_data import ticket_mix, ticket_sales, ticket_vs_goal

ticket_sales_daily = ticket_sales()
ticket_sales_mix = ticket_mix()
ticket_vs_goal = ticket_vs_goal()
