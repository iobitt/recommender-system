json.extract! order_line, :id, :account_id, :order_id, :product_id, :variant_id, :title, :quantity, :created_at, :updated_at
json.url order_line_url(order_line, format: :json)
