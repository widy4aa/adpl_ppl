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
        Schema::create('device_configurations', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('id_device_control');
            $table->float('suhu_min');
            $table->float('suhu_max');
            $table->float('kelembapan_min');
            $table->float('kelembapan_max');
            $table->float('kelembapan_tanah_min');
            $table->float('kelembapan_tanah_max');
            $table->boolean('mode_auto');
            $table->timestamp('updated_at');

            $table->foreign('id_device_control')->references('id')->on('device_controls')->onDelete('cascade')->onUpdate('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('device_configurations');
    }
};
