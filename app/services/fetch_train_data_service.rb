# frozen_string_literal: true

class FetchTrainDataService < ApplicationService
  attr_accessor :account

  def initialize(account)
    @account = account
  end

  def call
    [
      InsalesApi::Category,
      InsalesApi::Product,
      InsalesApi::Variant,
      InsalesApi::Order,
      InsalesApi::OrderLine
    ].each do |resource|
      raise 'inSales API not configured!' unless resource.init(account)
    end

    FetchService.call(account, InsalesApi::Category) do |category|
       account.categories.create(category.attributes)
    end

    FetchService.call(account, InsalesApi::Product) do |product|
      ActiveRecord::Base.transaction do
        account.products.create(product.attributes.slice(:id, :category_id, :title))
        product.attributes['variants'].each do |variant|
          account.variants.create(variant.attributes.slice(:id, :product_id, :title))
        end
      end
    end

    FetchService.call(account, InsalesApi::Order) do |order|
      ActiveRecord::Base.transaction do
        order_attributes = order.attributes.tap do |attributes|
          attributes[:client_id] = attributes['client'].attributes['id']
        end.slice(:id, :client_id, :total_price)
        account.orders.create(order_attributes)
        order.attributes['order_lines'].each do |order_line|
          account.order_lines.create(order_line.attributes.slice(:id, :order_id, :product_id, :variant_id, :title, :quantity))
        end
      end
    end
  end
end
