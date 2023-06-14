# frozen_string_literal: true

class InstallationsController < ApplicationController
  def install
    ExtraLogger.info('New installation', self.class, **permitted_params)
    Account.create!(permitted_params)
    head :ok
  end

  def enter
    redirect_to account_path(Account.find_by!(external_id: params[:insales_id]))
  end

  private

  def permitted_params
    params.permit(:shop, :insales_id, :token).tap do |params|
      params[:external_id] = params.delete(:insales_id)
      token = params.delete(:token)
      params[:password] = Digest::MD5.hexdigest(token + secret_key)
    end
  end

  def secret_key
    Rails.application.credentials.insales[:secret_key]
  end
end
