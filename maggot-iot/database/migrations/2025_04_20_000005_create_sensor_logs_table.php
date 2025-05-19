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
        Schema::create('sensor_logs', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('id_device');
            $table->float('kelembapan_udara');
            $table->float('kelembapan_tanah');
            $table->float('suhu_udara');
            $table->float('suhu_tanah');
            $table->timestamp('recorded_at');

            $table->foreign('id_device')->references('id')->on('device_ids')->onUpdate('cascade')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('sensor_logs');
    }
};
