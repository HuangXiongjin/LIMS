<template>
  <el-row :gutter="15">
    <el-col :span="4">
         <div class="platformContainer">
            <p class="marginBottom">选择要设置工序的品名</p>
            <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
            <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in results" :key="index" v-bind:effect="item.BrandName===BrandActive?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode)">{{item.BrandName}}</el-tag>
          </div>
    </el-col>
    <el-col :span='20'>
        <el-row>
          <el-col :span='24'>
            <div class="platformContainer">
              <p>当前选择的品名：{{BrandActive}}</p>
            </div>
            <div class="platformContainer">
              <div v-for="(item, index) in inProcessList" :key="index" class="list-complete-item" :data-idd="item.ID" style="display:inline-block;marginRight:18px;cursor:pointer" @click='showPGL(item.PUName,item.PUCode,index)'>
                    <div class="container-col" :class='{"pactive":index===ActiveIndex}'>
                      <span class="text-size-14">{{ item.PUName }}</span>
                    </div>
              </div>
            </div>
          </el-col>
          <el-col :span='24'>
            <div class='platformContainer' style='height:500px;'>
              <el-upload
                class="myupload"
                drag
                accept=".doc,.docx"
                action="/api/batchmodelexport"
                :limit="1"
                :on-preview="handlePreview"
                :before-remove="beforeRemove"
                :before-upload="handleBeforeUpload"
                :on-remove="handleRemove"
                :on-exceed="handleExceed"
                :on-success='submitSuccess'
                :on-error='submitError'
                :file-list="fileList">
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                <div slot="tip" class="el-upload__tip">只能上传.docx 批记录表</div>
              </el-upload>
            </div>
          </el-col>
        </el-row>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "BatchRecordFiles",
    data(){
      return {
          productName:'',
          results:[],
          BrandActive:'',
          BrandCode:'',
          PUCode:'',
          PUName:'',
          inProcessList:[],
          fileList: [],
          ActiveIndex:10,
          FileName:'',
          scheduleTableData:[]
      }
    },
    created(){
      this.getScheduleTableData()
    },
    methods:{
      handlePreview(file){
        var FileName=file.name
        var params={
          FileName:FileName
        }
         this.$confirm('是否下载该文件到本地?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          window.open("/api/ManualDownload?FileName="+FileName) //下载文件
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消下载'
          });          
        });        
      },
      showPGL(PUName,PUCode,e){ //点击工艺按钮 
        //发起请求获取当前工艺pgl
        this.PUName=PUName
        this.PUCode=PUCode
        this.ActiveIndex=e
        var params={
          PUCode:this.PUCode,
          BrandCode:this.BrandCode
        }
        this.axios.get('/api/batchmodelselect',{params:params}).then((res) => {
          if(res.data.code==='200'){
            this.fileList=res.data.message.map(item=>{
              return {name:item.FileName,url:item.FilePath,ID:item.ID}
            })
          }else{
             this.$message({
              type: 'error',
              message: '获取批记录文档失败'
            });
          }
        })
      },
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
      handleExceed(files, fileList) {
          this.$message({
          message: '限制只能上传一条数据',
          type: 'error'
        });
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      submitSuccess(){
          this.$message({
            message: "上传文件成功！",
            type: 'success'
        });
      },
      submitError(){
        this.$message({
          message:'上传失败，请重新上传文件',
          type:'error'
        })
      },
      handleBeforeUpload(file){
        var FileExt = file.name.replace(/.+\./, "");
        if (['doc', 'docx'].indexOf(FileExt.toLowerCase()) === -1){ 
          this.$message({ type: 'warning', message: '请上传后缀名为[doc,docx]的附件！' });
          return false; 
          }else{
            this.FileName=file.name
            var params={
              BrandName:this.BrandActive,
              BrandCode:this.BrandCode,
              PUCode:this.PUCode,
              PUIDName:this.PUName,
              FileName:this.FileName,
            }
            this.axios.post('/api/batchmodelinsert',this.qs.stringify(params)).then((res) => {
              if(res.data.code==='200'){
                this.showPGL(this.PUName,this.PUCode,this.ActiveIndex)
              }
            })
          }
            
      },
      handleRemove(file,fileList){
        var fileID=file.ID
        var params={
          id:fileID
        }
        this.axios.post('/api/ManualDelete',this.qs.stringify(params)).then((res) => {
          if(res.data.code==='200'){
             this.showPGL(this.PUName,this.PUCode,this.ActiveIndex)
          }
        })
      }
    }
  }
</script>

<style scoped>
  .container-col{
    clear: both;
    overflow: hidden;
    border:1px solid rgba(185,185,185,1);
    background:#fff;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
    height: 50px;
  }
  .pactive{
    background-color:rgba(211,237,239,1);
  }
</style>
