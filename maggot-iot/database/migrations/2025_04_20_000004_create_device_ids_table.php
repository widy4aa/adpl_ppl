<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('device_ids', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('id_kandang');
            $table->string('device_name');
            $table->foreign('id_kandang')->references('id')->on('kandangs')->onUpdate('cascade')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('device_ids');
    }
};
