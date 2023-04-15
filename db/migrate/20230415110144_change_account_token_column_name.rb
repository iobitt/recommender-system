class ChangeAccountTokenColumnName < ActiveRecord::Migration[7.0]
  def change
    rename_column :accounts, :token, :password
  end
end
