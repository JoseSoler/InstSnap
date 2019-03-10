import { Component, OnInit, Input } from '@angular/core';
import {Post} from '../Post';
import { PostsService } from '../posts.service';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.css']
})

export class PostComponent implements OnInit {
  posts: any = [];
  
  @Input() inquiry: any = {};

  constructor(public service:PostsService) { }

  ngOnInit() {
    this.getPosts();
  }

  getPosts() {
    this.posts = [];
    this.service.getAllPosts().subscribe((data: {}) => {
      console.log(data);
      this.posts = data;
    });
  }

  searchPosts() {
     console.log(this.inquiry);
     this.service.searchPosts(this.inquiry).subscribe((data: {}) => {
      console.log(data);
      this.posts = data;
    });
  }


}
