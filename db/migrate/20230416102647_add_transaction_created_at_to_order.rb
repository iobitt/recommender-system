class AddTransactionCreatedAtToOrder < ActiveRecord::Migration[7.0]
  def change
    add_column :orders, :transaction_created_at, :datetime, null: false
  end
end
