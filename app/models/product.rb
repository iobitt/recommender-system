class Product < ApplicationRecord
  validates :id, uniqueness: true
end
