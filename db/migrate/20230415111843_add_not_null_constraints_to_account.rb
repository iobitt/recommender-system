class AddNotNullConstraintsToAccount < ActiveRecord::Migration[7.0]
  def change
    change_column_null :accounts, :external_id, false
    change_column_null :accounts, :shop, false
    change_column_null :accounts, :password, false
  end
end
