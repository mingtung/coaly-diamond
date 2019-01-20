<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr><br><br>
        <alert :message="message" v-if="showMessage"></alert>
        <button type="button"
                class="btn btn-success btn-sm"
                v-b-modal.book-modal>Add Book
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Read?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>
                <span v-if="book.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.book-modal
                        @click="onEditBook(book)">Update
                </button>
                <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteBook(book)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addBookModal"
             id="book-modal"
             hide-footer>
      <div slot="modal-title">{{ bookModalTitle }}</div>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addBookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addBookForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addBookForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      books: [],
      addBookForm: {
        id: '',
        title: '',
        author: '',
        read: [],
      },
      bookModalTitle: 'Add a new book',
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000/books';
      axios
        .get(path)
        .then(res => {
          this.books = res.data.books;
        })
        .catch(error => {
          console.log(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios
        .post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book added!';
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getBooks();
          this.message = 'Something went wrong when adding the book:(';
          this.showMessage = true;
        });
    },
    updateBook(payload, bookId) {
      const path = `http://localhost:5000/books/${bookId}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book updated!';
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getBooks();
          this.message = 'Something went wrong when updating the book:(';
          this.showMessage = true;
        });
    },
    deleteBook(bookId) {
      const path = `http://localhost:5000/books/${bookId}`;
      axios
        .delete(path)
        .then(() => {
          this.getBooks();
          this.message = 'Book deleted!';
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getBooks();
          this.message = 'Something went wrong when deleting the book:(';
          this.showMessage = true;
        });
    },
    onEditBook(book) {
      this.addBookForm = book;
      this.bookModalTitle = 'Edit the book';
    },
    onDeleteBook(book) {
      this.deleteBook(book.id);
      this.initForm();
    },
    initForm() {
      this.addBookForm.id = '';
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.read = [];
      this.bookModalTitle = 'Add a new book';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      let read = false;
      if (this.addBookForm.read[0]) {
        read = true;
      }
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        read,
      };
      if (this.addBookForm.id !== '') {
        this.updateBook(payload, this.addBookForm.id);
      } else {
        this.addBook(payload);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getBooks();
  },
};
</script>
