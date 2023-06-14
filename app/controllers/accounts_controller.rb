# frozen_string_literal: true

class AccountsController < ApplicationController
  helper_method :account

  def start_train
    FetchTrainDataService.call(account)
    head :ok
  end

  def account
    @account ||= Account.find(params[:id])
  end
end
