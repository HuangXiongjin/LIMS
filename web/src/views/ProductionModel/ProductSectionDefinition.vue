<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span>产品定义工艺段</span>
      </div>
      <el-row :gutter="15">
        <el-col :span="4">
          <div class="platformContainer">
            <p class="marginBottom">选择要设置工序的品名</p>
            <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
            <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in results" :key="index" v-bind:effect="item.BrandName===BrandActive?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode)">{{item.BrandName}}</el-tag>
          </div>
        </el-col>
        <el-col :span="20">
          <el-row>
            <el-col :span="24">
              <div class="platformContainer">
                <p class="marginBottom">全部工序 <span class="text-size-12 color-grayblack">拖动工序到虚线框内来设置产品的工序</span></p>
                <draggable :list="processList" v-bind="{group:{name: flags,pull:'clone'}, sort: true}"
                  @end="end" class="dragArea">
                  <div v-for="(item,index) in processList" :key="index" class="list-complete-item" :data-pcode="item.PUCode" :data-pname="item.PUName">
                    <div class="container-col">
                      <span class="text-size-14">{{ item.PUName }}</span>
                    </div>
                  </div>
                </draggable>
              </div>
            </el-col>
            <el-col :span="24" v-if="BrandActive">
              <div class="platformContainer">
                <p class="marginBottom">
                  <span>{{ BrandActive }}</span>的工序 <span class="text-size-12 color-grayblack">请按照工艺顺序排列，如遇到顺序号相同时，可原处拖动一下，将会自动修改。</span>
                </p>
                <draggable :list="inProcessList" v-bind="{group:'article', disabled: disabled,sort: true}"
                   @start="start22"
                   @end="end22" class="dragArea11" style="border: 1px dashed #B9B9B9;padding: 10px;">
                  <div v-for="(item, index) in inProcessList" :key="index" class="list-complete-item" :data-idd="item.ID">
                    <div class="container-col">
                      <span class="text-size-14">{{ item.PUName }}</span>
                      <i class="el-icon-delete" @click="handleDel(index, item.ID)"></i>
                    </div>
                  </div>
                </draggable>
              </div>
            </el-col>
            <el-col :span="24">
              <div class="platformContainer">
                <p class="marginBottom">表格数据</p>
                <el-table :data="inProcessList" border size="small">
                  <el-table-column prop="BrandName" label="品名"></el-table-column>
                  <el-table-column prop="PUName" label="工艺段名称"></el-table-column>
                  <el-table-column prop="Seq" label="顺序号"></el-table-column>
                </el-table>
              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  import draggable from 'vuedraggable'
  export default {
    name: "ProductSectionDefinition",
    components:{draggable},
    data(){
      return{
        scheduleTableData:[],
        results:[],
        productName:"",
        BrandActive:"",
        BrandCode:"",
        flags: 'article',
        disabled: false,
        processList:[],
        inProcessList:[],
      }
    },
    mounted(){
      this.getScheduleTableData()
      this.getProcessTableData()
    },
    methods:{
      getScheduleTableData(){ //获取品名
        var that = this
        var params = {
          tableName: "ProductRule",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.scheduleTableData = res.data.data.rows
            that.results = that.scheduleTableData
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleChangeProductName(queryString){
        if(queryString != ""){
          this.results = this.scheduleTableData.filter((string) =>{
            return Object.keys(string).some(function(key) {
              return String(string[key]).toLowerCase().indexOf(queryString) > -1
            })
          })
        }else{
          this.results = this.scheduleTableData
        }
      },
      clickBrandTag(BrandName,BrandCode){
        this.BrandActive = BrandName
        this.BrandCode = BrandCode
        this.getBrandProcessTableData(BrandName)
      },
      getBrandProcessTableData(BrandName){ //查询当前品名绑定的工序
        var that = this
        var params = {
          tableName: "ProductUnit",
          field:"BrandName",
          fieldvalue:BrandName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            function compare(property){
              return function(a,b){
                var value1 = a[property];
                var value2 = b[property];
                return value1 - value2;
              }
            }
            that.inProcessList = res.data.data.rows.sort(compare('Seq'))
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      getProcessTableData(){ //获取所有工序
        var that = this
        var params = {
          tableName: "ProcessUnit",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.processList = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      end (ev) {
        //判断是否拖进了品名工序的范围
        if (ev.to.className === 'dragArea11') {
          this.$set(this.processList[ev.oldIndex], 'flags', true)
          var PUCode = ev.clone.attributes['data-pcode'].value
          var PUName = ev.clone.attributes['data-pname'].value
          var params = {
            tableName:"ProductUnit",
            PUCode:PUCode,
            PUName:PUName,
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode,
            Seq:ev.newIndex
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.getBrandProcessTableData(this.BrandActive)
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }
      },
      start22 (event) {
        this.flags = '222222'
      },
      end22 (ev) {
        this.flags = 'article'
        //修改产品工序的顺序
        var idd = ev.clone.attributes['data-idd'].value
        var params = {
          tableName:"ProductUnit",
          ID:idd,
          Seq:ev.newIndex,
        }
        this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
          if(res.data.code === "200"){
            this.$message({
              type: 'success',
              message: res.data.message
            });
            this.getBrandProcessTableData(this.BrandActive)
          }else{
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
        },res =>{
          console.log("请求错误")
        })
      },
      handleDel (index, id) {
        this.inProcessList.splice(index, 1)
        var params = {
          tableName:"ProductUnit",
          delete_data:"[{id:" + id + "}]"
        }
        this.axios.delete("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            this.$message({
              type: 'success',
              message: res.data.message
            });
            this.getBrandProcessTableData(this.BrandActive)
          }
        },res =>{
          console.log("请求错误")
        })
      },
    }
  }
</script>

<style scoped>
  .container-col{
    clear: both;
    overflow: hidden;
    border:1px solid rgba(185,185,185,1);
    background:rgba(211,237,239,1);
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
    height: 50px;
  }
  .list-complete-item {
    cursor: pointer;
    position: relative;
    width: 120px;
    display: inline-block;
    margin-right: 15px;
  }
  .list-complete-item.sortable-chosen {
    color: #4AB7BD;
  }
  .list-complete-item.sortable-ghost {
    color: #30B08F;
  }
  .dragArea11{
    height: 70px;
  }
  .list-complete-enter,.list-complete-leave-active {
    opacity: 0;
  }
</style>
