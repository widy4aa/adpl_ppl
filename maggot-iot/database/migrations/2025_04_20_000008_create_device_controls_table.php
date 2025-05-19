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
        Schema::create('device_controls', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('id_device');
            $table->foreign('id_device')->references('id')->on('device_ids')->onUpdate('cascade')->onDelete('cascade');
            $table->enum('mode', ['manual', 'otomatis']);
            $table->enum('status', ['on', 'off']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('device_controls');
    }
};
