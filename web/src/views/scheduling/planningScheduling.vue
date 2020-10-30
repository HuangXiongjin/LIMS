<template>
  <div>
    <el-button type="primary" @click="Ad1">审核</el-button>
    <el-button type="primary" @click="Ad2">选择设备</el-button>
    <el-button type="primary" @click="Ad3">下发计划</el-button>

  </div>
</template>
<script>
export default {
  data(){
    return {

    }

  },
  methods: {
    Ad1() {
      this.$router.push('/CheckscPlan')
    },
    Ad2(){
      this.$router.push('/EquipmentChoose')
    },
    Ad3(){
      this.$router.push('/DistributionPlan')
    },

  },
}
</script>
